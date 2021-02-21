package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class TheAlexaSkillApp {
    public static void main(final String[] args) {
        App app = new App();

        new TheAlexaSkillStack(app, "TheAlexaSkillStack");

        app.synth();
    }
}
