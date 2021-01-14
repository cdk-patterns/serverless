package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheDynamodbAtomicCounterApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheDynamodbAtomicCounterStack(app, "TheDynamodbAtomicCounterStack");

        app.synth();
    }
}
