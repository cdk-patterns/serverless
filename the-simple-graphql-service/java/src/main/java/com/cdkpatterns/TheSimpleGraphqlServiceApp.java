package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheSimpleGraphqlServiceApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheSimpleGraphqlServiceStack(app, "TheSimpleGraphqlServiceStack");

        app.synth();
    }
}
