using NLog;
using System;
using System.Runtime.Loader;
using System.Threading;

namespace GracefulShutdown
{
    class Program
    {
        /// <summary>
        /// 
        /// </summary>
        static Logger _logger = LogManager.GetCurrentClassLogger(typeof(Program));

        /// <summary>
        /// 
        /// </summary>
        static bool _sigintReceived = false;

        /// <summary>
        /// 
        /// </summary>
        static void Main(string[] args)
        {
            Console.WriteLine("begin to init ...");
            _logger.Info("begin to init ...");
            AssemblyLoadContext.Default.Unloading += ctx =>
            {
                if (!_sigintReceived)
                {
                    _logger.Info("recieved SIGTERM#1");
                    _sigintReceived = true;
                }
                else
                {
                    _logger.Info("get SIGTERM，skip SIGTERM");
                }
            };

            AppDomain.CurrentDomain.ProcessExit += (sender, e) =>
            {
                if (!_sigintReceived)
                {
                    _logger.Info("recieved SIGTERM#2");
                    _sigintReceived = true;
                }
                else
                {
                    _logger.Info("get SIGTERM，skip SIGTERM");
                }
            };

            Console.CancelKeyPress += (sender, e) =>
            {
                e.Cancel = true;
                Console.WriteLine("get SIGINT from (Ctrl+C)");
                _logger.Info("get SIGINT from (Ctrl+C)");
                _sigintReceived = true;
            };

            _logger.Info("init completed");
            while (!_sigintReceived)
            {
                Thread.Sleep(1000);
            }

            const int QUIT_MORE_WAIT_SECS = 5;
            _logger.Info($"wait {QUIT_MORE_WAIT_SECS} secs to prepare quit the application");
            Thread.Sleep(QUIT_MORE_WAIT_SECS * 1000);
            _logger.Info($"All over");
        }
    }
}
