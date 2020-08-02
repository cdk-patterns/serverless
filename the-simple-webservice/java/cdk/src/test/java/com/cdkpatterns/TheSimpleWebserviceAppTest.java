package com.cdkpatterns;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.junit.jupiter.api.Test;
import software.amazon.awscdk.core.App;

public class TheSimpleWebserviceAppTest {
    private final static ObjectMapper JSON =
            new ObjectMapper().configure(SerializationFeature.INDENT_OUTPUT, true);

    @Test
    public void testStack() {
        App app = new App();
        TheSimpleWebserviceStack stack = new TheSimpleWebserviceStack(app, "test");

        JsonNode actualStack = JSON.valueToTree(app.synth().getStackArtifact(stack.getArtifactId()).getTemplate());
    }
}
