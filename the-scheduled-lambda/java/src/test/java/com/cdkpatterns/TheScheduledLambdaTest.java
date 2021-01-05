package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import com.cdkpatterns.TheScheduledLambdaStack;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.IOException;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

public class TheScheduledLambdaTest {
    private final static ObjectMapper JSON =
        new ObjectMapper().configure(SerializationFeature.INDENT_OUTPUT, true);

    @Test
    public void testStack() throws IOException {
        App app = new App();
        TheScheduledLambdaStack stack = new TheScheduledLambdaStack(app, "test");

        // synthesize the stack to a CloudFormation template and compare against
        // a checked-in JSON file.
        JsonNode actual = JSON.valueToTree(app.synth().getStackArtifact(stack.getArtifactId()).getTemplate());

        // After Synth, performs some basic tests

        // AWS::Events::Rule exists test
        assertThat(actual.toString()).contains("AWS::Events::Rule");

        // AWS::Lambda::Function exists test
        assertThat(actual.toString()).contains("AWS::Lambda::Function");

        // AWS::DynamoDB::Table exists test
        assertThat(actual.toString()).contains("AWS::DynamoDB::Table");
    }
}
