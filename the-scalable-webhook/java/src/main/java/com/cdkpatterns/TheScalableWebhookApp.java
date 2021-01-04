package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheScalableWebhookApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheScalableWebhookStack(app, "TheScalableWebhookStack");

        app.synth();
    }
}
