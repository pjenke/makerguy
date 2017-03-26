//
//  ViewController.swift
//  RobotController
//
//  Created by Philipp Jenke on 31.12.16.
//  Copyright © 2016 Philipp Jenke. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    private var moveA = 0.0;
    private var moveB = 0.0;
    private let ip = "192.168.2.100:1234";
    
    override func viewDidLoad() {
        super.viewDidLoad()
        var _ = Timer.scheduledTimer(timeInterval: 0.5, target: self, selector: #selector(self.update), userInfo: nil, repeats: true);
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    @IBAction func start(_ sender: UIButton) {
        moveA = 1;
        moveB = 1;
    }
    
    @IBAction func stop(_ sender: UIButton) {
        moveA = 0;
        moveB = 0;
    }
    
    func update() {
        let url = "http://" + ip + "/robot?moveA=" + String(moveA) + "&moveB=" + String(moveB)
        print(url)
        HttpRequest.post(url:url, errorHandler:{()->Void in print("Error!")})
    }
    
    @IBAction func turn(_ sender: UISlider) {
        if ( moveA + moveB < 0.5 ){
            return;
        }
        let turnValue = ((sender.value - sender.minimumValue)/(sender.maximumValue-sender.minimumValue) - 0.5) * 2.0;
        moveA = 1.0;
        moveB = 1.0;
        if ( turnValue < 0){
            // turn left
            moveA = 1.0 - (Double)(turnValue * -1);
        } else {
            // turn right
            moveB = 1.0 - (Double)(turnValue);
        }
    }
}

