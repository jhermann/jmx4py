/*
    Copyright 2011 Juergen Hermann

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

package org.jolokia.jmx4py.testjvm;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.lang.management.ManagementFactory;


/**
 *  Application to start a test JVM and keep it open until stopped.
 *
 */
public class App {
    private static String jvm_id = "N/A";
    
    public static void main(String[] args) {
        if (args.length == 0) {
            fail("Provide the path to a guard file!");
        }
        jvm_id = ManagementFactory.getRuntimeMXBean().getName();
        
        File guard = new File(args[0]);
        createGuard(guard);
        guard.deleteOnExit();

        System.out.println("Waiting for guard file '" + guard + "' of JVM " + jvm_id + " to disappear...");
        while (guard.exists()) {
            try {
                Thread.sleep(1000L);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Guard file gone, test JVM " + jvm_id + " exiting...");
    }

    
    /**
     * @param guard
     */
    private static void createGuard(File guard) {
        OutputStreamWriter out = null;
        try {
            out = new OutputStreamWriter(new FileOutputStream(guard), "UTF-8");
        } catch (UnsupportedEncodingException e) {
            fail("Punt! JVM is broken!");
        } catch (FileNotFoundException e) {
            fail("Bad guard file path: " + guard);
        }
        try {
            try {
                out.write(jvm_id + "\n");
            } catch (IOException e) {
                fail("Cannot write to guard file: " + guard);
            }
        } finally {
            try {
                out.close();
            } catch (IOException e) {
                fail("Cannot write to guard file: " + guard);
            }
        }
    }

    
    /**
     * @param msg
     */
    private static void fail(String msg) {
        System.out.println(msg);
        System.exit(1);
    }
}
