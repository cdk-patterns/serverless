package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheLambdaPowerTunerApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheLambdaPowerTunerStack(app, "TheLambdaPowerTunerStack");

        app.synth();
    }
}
