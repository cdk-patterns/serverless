using Amazon.CDK;

namespace TheEventbridgeAtm
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheEventbridgeAtmStack(app, "TheEventbridgeAtmStack");

            app.Synth();
        }
    }
}
