using Amazon.CDK;

namespace TheSimpleWebservice
{
    public class Program
    {
        public static void Main()
        {
            var app = new App();
            new TheSimpleWebserviceStack(app, "TheSimpleWebserviceStack");
            app.Synth();
        }
    }
}
