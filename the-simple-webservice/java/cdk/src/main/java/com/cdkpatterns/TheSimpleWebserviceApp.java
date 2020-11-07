package com.cdkpatterns;

import software.amazon.awscdk.core.App;

public class TheSimpleWebserviceApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheSimpleWebserviceStack(app, "TheSimpleWebserviceStack");

        app.synth();
    }
}
