package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheScheduledLambdaApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheScheduledLambdaStack(app, "TheScheduledLambdaStack");

        app.synth();
    }
}
