package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class PollyApp {
    public static void main(final String[] args) {
        App app = new App();

        new PollyStack(app, "PollyStack");

        app.synth();
    }
}
