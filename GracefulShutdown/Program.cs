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
            AssemblyLoadContext.Default.Unloading += ctx =>
            {
                if (!_sigintReceived)
                {
                    _logger.Info("recieved SIGTERM");
                }
                else
                {
                    _logger.Info("[AssemblyLoadContext.Default.Unloading] get SIGINT，skip SIGTERM");
                }
            };

            AppDomain.CurrentDomain.ProcessExit += (sender, e) =>
            {
                if (!_sigintReceived)
                {
                    _logger.Info("已接收 SIGTERM");
                }
                else
                {
                    _logger.Info("[AppDomain.CurrentDomain.ProcessExit] get SIGINT，skip SIGTERM");
                }
            };

            Console.CancelKeyPress += (sender, e) =>
            {
                e.Cancel = true;
                _logger.Info("get SIGINT from (Ctrl+C)");
                _sigintReceived = true;
            };

            
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
