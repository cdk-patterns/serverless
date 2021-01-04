package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheStateMachineApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheStateMachineStack(app, "TheStateMachineStack");

        app.synth();
    }
}
