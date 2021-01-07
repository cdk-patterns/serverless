package com.cdkpatterns;

import software.amazon.awscdk.core.App;

import com.cdkpatterns.TheEfsLambdaStack;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.IOException;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

public class TheEfsLambdaTest {
    private final static ObjectMapper JSON =
        new ObjectMapper().configure(SerializationFeature.INDENT_OUTPUT, true);

    @Test
    public void testStack() throws IOException {
        App app = new App();
        TheEfsLambdaStack stack = new TheEfsLambdaStack(app, "test");

        // synthesize the stack to a CloudFormation template and compare against
        // a checked-in JSON file.
        JsonNode actual = JSON.valueToTree(app.synth().getStackArtifact(stack.getArtifactId()).getTemplate());

        // After synth, performs some basic tests
        
        // AWS::EC2::VPC exists test
        assertThat(actual.toString()).contains("AWS::EC2::VPC");
        
        // AWS::EFS::AccessPoint exists test
        assertThat(actual.toString()).contains("AWS::EFS::AccessPoint");
        
        // AWS::EFS::FileSystem exists test
        assertThat(actual.toString()).contains("AWS::EFS::FileSystem");
        
    }
}
