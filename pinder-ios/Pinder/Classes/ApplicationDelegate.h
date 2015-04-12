//
//  ApplicationDelegate.h
//
//  Created by Sergey Tkachenko on 2/6/14.
//  Copyright © 2014 Exadel Inc. All rights reserved.
//

#import <Cordova/CDVViewController.h>
#import <Cordova/CDVCommandDelegateImpl.h>
#import <Cordova/CDVCommandQueue.h>

@interface ApplicationDelegate : NSObject < UIApplicationDelegate >

@property (nonatomic, strong) IBOutlet UIWindow* window;
@property (nonatomic, strong) IBOutlet CDVViewController* viewController;

@end
