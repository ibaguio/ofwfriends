//
//  ApplicationDelegate.m
//
//  Created by Sergey Tkachenko on 2/6/14.
//  Copyright © 2014 Exadel Inc. All rights reserved.
//

#import "ApplicationDelegate.h"
#import "MainViewController.h"

#import <Cordova/CDVPlugin.h>
#import <Cordova/CDVURLProtocol.h>

#ifdef USE_PUSH_NOTIFICATION_PLUGIN
#import "PushNotification.h"
#endif

#import "WebProjectInfo.h"

@implementation ApplicationDelegate

@synthesize window, viewController;

- (id)init
{
    if(self = [super init])
    {
        NSHTTPCookieStorage *cookieStorage = [NSHTTPCookieStorage sharedHTTPCookieStorage];
        [cookieStorage setCookieAcceptPolicy:NSHTTPCookieAcceptPolicyAlways];

        int cacheSizeMemory = 8 * 1024 * 1024;  //  8MB
        int cacheSizeDisk = 32 * 1024 * 1024;   // 32MB

        NSURLCache* sharedCache = [[NSURLCache alloc] initWithMemoryCapacity:cacheSizeMemory diskCapacity:cacheSizeDisk diskPath:@"nsurlcache"];
        [NSURLCache setSharedURLCache:sharedCache];
    }

    return self;
}


#pragma mark - UIApplicationDelegate implementation

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    CGRect screenBounds = [[UIScreen mainScreen] bounds];
    self.window = [[UIWindow alloc] initWithFrame:screenBounds];
    self.window.autoresizesSubviews = YES;

    self.viewController = [[MainViewController alloc] init];

    // Retreive information about web project.
    WebProjectInfo *webProjectInfo = [[WebProjectInfo alloc] init];

    self.viewController.wwwFolderName = [webProjectInfo folderPath];
    NSLog(@"ProjectFolder: %@",self.viewController.wwwFolderName);

    self.viewController.startPage = [webProjectInfo startPageName];
    NSLog(@"StartPage: %@", self.viewController.startPage);

    // check whether the current orientation is supported: if it is, keep it, rather than forcing a rotation
    UIInterfaceOrientation curDevOrientation = [[UIApplication sharedApplication] statusBarOrientation];

    BOOL forceStartupRotation = ![self.viewController supportsOrientation: curDevOrientation];
    if(forceStartupRotation)
    {
        // The first item in the supportedOrientations array is the start orientation (guaranteed to be at least Portrait)
        UIInterfaceOrientation newOrient = UIInterfaceOrientationPortrait;
        [[UIApplication sharedApplication] setStatusBarOrientation:newOrient];
    }

    self.window.rootViewController = self.viewController;
    [self.window makeKeyAndVisible];

#ifdef USE_PUSH_NOTIFICATION_PLUGIN
    // PushNotification - Handle launch from a push notification
    NSDictionary *userInfo = [launchOptions objectForKey:UIApplicationLaunchOptionsRemoteNotificationKey];
    if(userInfo) {
        PushNotification *pushHandler = [self.viewController getCommandInstance:@"PushNotification"];
        NSMutableDictionary *mutableUserInfo = [userInfo mutableCopy];
        [mutableUserInfo setValue:@"1" forKey:@"applicationLaunchNotification"];
        [mutableUserInfo setValue:@"0" forKey:@"applicationStateActive"];
        [pushHandler.pendingNotifications addObject:mutableUserInfo];
    }
#endif

    return YES;
}

- (BOOL)application:(UIApplication *)application handleOpenURL:(NSURL *)url
{
    if(!url)
    {
        return NO;
    }

    // calls into javascript global function 'handleOpenURL'
    NSString *jsString = [NSString stringWithFormat:@"handleOpenURL(\"%@\");", url];
    [self.viewController.webView stringByEvaluatingJavaScriptFromString:jsString];

    // all plugins will get the notification, and their handlers will be called
    [[NSNotificationCenter defaultCenter] postNotification:[NSNotification notificationWithName:CDVPluginHandleOpenURLNotification object:url]];

    return YES;
}

- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application
{
    [[NSURLCache sharedURLCache] removeAllCachedResponses];
}

#ifdef USE_PUSH_NOTIFICATION_PLUGIN

#pragma mark - PushNotification delegation

- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken
{
    PushNotification* pushHandler = [self.viewController getCommandInstance:@"PushNotification"];
    [pushHandler didRegisterForRemoteNotificationsWithDeviceToken:deviceToken];
}

- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)error
{
    PushNotification *pushHandler = [self.viewController getCommandInstance:@"PushNotification"];
    [pushHandler didFailToRegisterForRemoteNotificationsWithError:error];
}

- (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo
{
    PushNotification *pushHandler = [self.viewController getCommandInstance:@"PushNotification"];
    NSMutableDictionary *mutableUserInfo = [userInfo mutableCopy];

    // Get application state for iOS4.x+ devices, otherwise assume active
    UIApplicationState appState = UIApplicationStateActive;
    if ([application respondsToSelector:@selector(applicationState)])
    {
        appState = application.applicationState;
    }

    [mutableUserInfo setValue:@"0" forKey:@"applicationLaunchNotification"];

    if (appState == UIApplicationStateActive)
    {
        [mutableUserInfo setValue:@"1" forKey:@"applicationStateActive"];
        [pushHandler didReceiveRemoteNotification:mutableUserInfo];
    }
    else
    {
        [mutableUserInfo setValue:@"0" forKey:@"applicationStateActive"];
        [mutableUserInfo setValue:[NSNumber numberWithDouble: [[NSDate date] timeIntervalSince1970]] forKey:@"timestamp"];
        [pushHandler.pendingNotifications addObject:mutableUserInfo];
    }
}

#endif

@end
