//
//  HttpRequest.swift
//  RCBoat
//
//  Created by Philipp Jenke on 12.06.15.
//  Copyright © 2015 Philipp Jenke. All rights reserved.
//

import Foundation

class HttpRequest {
    
    /* Send a post request */
    class func post(url:String, errorHandler:@escaping ()->()){
        let request : NSMutableURLRequest = NSMutableURLRequest()
        request.url = NSURL(string: url) as URL?
        request.httpMethod = "POST"
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        let task : URLSessionDataTask = session.dataTask(with: request as URLRequest, completionHandler: {(data, response, error) in
            if error != nil {
                errorHandler()
            }
            
        });
        
//        let session = NSURLSession.sharedSession()
//        let task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
//            if error != nil {
//                errorHandler()
//            }
//        })
        task.resume()
    }
    
    /* Send a GET request and handle the result in a closure handler */
//    class func get(url:String, resultHandler: (NSData?) -> Void, errorHandler:()->()){
//        let request : NSMutableURLRequest = NSMutableURLRequest()
//        request.URL = NSURL(string: url)
//        request.HTTPMethod = "GET"
//        let config = NSURLSessionConfiguration.defaultSessionConfiguration()
//        let session = NSURLSession(configuration: config)
//        let task : NSURLSessionDataTask = session.dataTaskWithRequest(request, completionHandler: {(data, response, error) in
//            if ( error != nil ){
//                print("Failed to get request result for url " + url)
//                errorHandler()
//            } else {
//                if let data2 = data {
//                    resultHandler(data2)
//                } else {
//                    print("Failed to get request result for url " + url)
//                }
//            }
//        });
    
        
//        let session = NSURLSession.sharedSession()
//        let task = session.dataTaskWithRequest(request){data, response, error -> Void in
//            if ( error != nil ){
//                print("Failed to get request result for url " + url)
//                errorHandler()
//            } else {
//                if let data2 = data {
//                    resultHandler(data2)
//                } else {
//                    print("Failed to get request result for url " + url)
//                }
//            }
//        }
//        task.resume()
//    }

    /* Convert NSData -> String */
//    class func data2String(data: NSData) -> NSString {
//        if let text = NSString(data: data, encoding:NSUTF8StringEncoding){
//            return text
//        }
//        return ""
//    }
}
