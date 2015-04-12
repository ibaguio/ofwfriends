//
//  MainViewController.h
//
//  Created by Sergey Tkachenko on 2/6/14.
//  Copyright © 2014 Exadel Inc. All rights reserved.
//

#import "MainViewController.h"
#import "ApperyioURLProtocol.h"

#import <AVFoundation/AVFoundation.h>

@interface MainViewController ()

@property (nonatomic, assign) CGFloat statusBarHeight;
@property (nonatomic, assign) BOOL initializeCompleted;
@property (nonatomic, strong) NSURLRequest *delayedRequest;
@property (nonatomic, strong) id rotationObserver;

/**
 * Register ApperyioURLProtocol to configure server trust authentication chalenge
 *     for allow or reject self-signed certificates.
 * This method should be invoked after [CDVViewController viewDidLoad] method
 *     to place ApperyioURLProtocol behind CDVURLProtocol.
 */
- (void)registerCustomURLProtocol;
- (void)unregisterCustomURLProtocol;

@end

@implementation MainViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    if(self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])
    {
        self.statusBarHeight = [[UIApplication sharedApplication] statusBarFrame].size.height;
        self.initializeCompleted = NO;
        self.delayedRequest = nil;
    }

    return self;
}

- (void)dealloc
{
    [[NSNotificationCenter defaultCenter] removeObserver:self];
    [self unregisterCustomURLProtocol];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    [self registerCustomURLProtocol];
    [self allowBackgroundAudioPlay];
    
    self.initializeCompleted = YES;
    
    if(nil != self.delayedRequest)
    {
        [self.webView loadRequest:self.delayedRequest];
        self.delayedRequest = nil;
    }
}

- (void) viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    [[NSNotificationCenter defaultCenter] removeObserver:self.rotationObserver];
    self.rotationObserver = nil;
}

- (void) viewDidDisappear:(BOOL)animated
{
    [super viewDidDisappear:animated];
    //ETST-14838
    if (SYSTEM_VERSION_LESS_THAN(@"7.0"))
    {
        self.rotationObserver = [[NSNotificationCenter defaultCenter] addObserverForName:UIDeviceOrientationDidChangeNotification
                                                                                  object:nil
                                                                                   queue:[NSOperationQueue mainQueue]
                                                                              usingBlock:^(NSNotification *note) {
                                                                                  CGSize screen = [[UIScreen mainScreen] bounds].size;
                                                                                  CGFloat statusBarHeight = [UIApplication sharedApplication].statusBarHidden ? 0 : self.statusBarHeight;
                                                                                  UIInterfaceOrientation orientation = [[UIApplication sharedApplication] statusBarOrientation];
                                                                                  if (UIDeviceOrientationIsPortrait(orientation))
                                                                                  {
                                                                                      self.view.frame = CGRectMake(0, 0, screen.width, screen.height - statusBarHeight);
                                                                                  }
                                                                                  else
                                                                                  {
                                                                                      self.view.frame = CGRectMake(0, 0, screen.height, screen.width - statusBarHeight);
                                                                                  }
                                                                              }];
    }
}

#pragma mark - Overwrite CDVViewController methods

- (NSArray*)parseInterfaceOrientations:(NSArray*)orientations
{
    if ((orientations == nil) || ([orientations count] == 0))
    {
        NSString* orientationString = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"UIInterfaceOrientation"];
        
        if (orientationString)
        {
            orientations = [NSArray arrayWithObject:orientationString];
        }
    }
    
    return [super parseInterfaceOrientations:orientations];
}

#pragma mark - UIWebViewDelegate

- (BOOL)webView:(UIWebView*)theWebView shouldStartLoadWithRequest:(NSURLRequest*)request navigationType:(UIWebViewNavigationType)navigationType
{
    if(self.initializeCompleted)
    {
        return [super webView:theWebView shouldStartLoadWithRequest:request navigationType:navigationType];
    }
    
    self.delayedRequest = request;

    return NO;
}

- (void)webView:(UIWebView*)theWebView didFailLoadWithError:(NSError*)error
{
    [super webView:theWebView didFailLoadWithError:error];
    
    //Temporary fix for ETST-16725
    if ([error code] == NSURLErrorCancelled)
    {
        [[NSNotificationCenter defaultCenter] postNotification:[NSNotification notificationWithName:CDVPageDidLoadNotification object:self.webView]];
    }
}

#pragma mark - Utility methods

- (void)registerCustomURLProtocol
{
    BOOL allowAllCertificates = [(NSNumber *)[self.settings objectForKey:@"AllowAllHTTPSCertificates"] boolValue];
    [ApperyioURLProtocol registerWithWhiteList:self.whitelist allowAllCertificates:allowAllCertificates];
}

- (void)unregisterCustomURLProtocol
{
    [ApperyioURLProtocol unregisterClass:[ApperyioURLProtocol class]];
}

- (void)allowBackgroundAudioPlay
{
    NSError *setBackgroundAudioPlayError = nil;
    
    [[AVAudioSession sharedInstance] setCategory:AVAudioSessionCategoryPlayback error:&setBackgroundAudioPlayError];
    if (setBackgroundAudioPlayError != nil)
    {
        NSLog(@"Cannot activate audio background playing due to error: %@.", setBackgroundAudioPlayError);
        return;
    }
}

@end
