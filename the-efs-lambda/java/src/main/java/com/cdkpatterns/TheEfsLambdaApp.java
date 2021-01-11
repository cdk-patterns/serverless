package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheEfsLambdaApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheEfsLambdaStack(app, "TheEfsLambdaStack");

        app.synth();
    }
}
