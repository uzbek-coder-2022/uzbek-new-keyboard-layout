// Uzbek-Keyboard-Setup.exe — yagona fayl o'rnatuvchi.
// Ichiga Setup.ps1 va bin\x64, bin\x86 dagi DLL'lar joylangan (embedded resource).
// Ishga tushganda vaqtinchalik papkaga ochadi, Setup.ps1 ni (oyna bilan) ishga tushiradi,
// tugagach papkani o'chiradi. Administrator huquqi manifest orqali so'raladi (UAC).
//
//   Uzbek-Keyboard-Setup.exe                                   -> oyna (UI)
//   Uzbek-Keyboard-Setup.exe -Action Install -Layout uzq,uzcw  -> buyruq satri
//   Uzbek-Keyboard-Setup.exe -Action Uninstall -Layout uzq,uzcw
//   Uzbek-Keyboard-Setup.exe --extract C:\papka                -> faqat fayllarni ochish
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Text;
using System.Windows.Forms;

static class Program
{
    static void Extract(string dir)
    {
        Assembly asm = Assembly.GetExecutingAssembly();
        foreach (string name in asm.GetManifestResourceNames())
        {
            string rel = name.Replace('/', Path.DirectorySeparatorChar);
            string target = Path.Combine(dir, rel);
            Directory.CreateDirectory(Path.GetDirectoryName(target));
            using (Stream s = asm.GetManifestResourceStream(name))
            using (FileStream f = File.Create(target))
            {
                s.CopyTo(f);
            }
        }
    }

    static string Quote(string a)
    {
        return (a.Length > 0 && a.IndexOfAny(new[] { ' ', '\t', '"' }) < 0) ? a : "\"" + a.Replace("\"", "\\\"") + "\"";
    }

    [STAThread]
    static int Main(string[] args)
    {
        if (args.Length == 2 && args[0] == "--extract")
        {
            Extract(args[1]);
            return 0;
        }

        string dir = Path.Combine(Path.GetTempPath(), "uzbek-kbd-" + Guid.NewGuid().ToString("N").Substring(0, 8));
        try
        {
            Extract(dir);

            bool gui = args.Length == 0;
            StringBuilder cmd = new StringBuilder("-NoProfile -ExecutionPolicy Bypass");
            if (gui) cmd.Append(" -WindowStyle Hidden");
            cmd.Append(" -File ").Append(Quote(Path.Combine(dir, "Setup.ps1")));
            foreach (string a in args) cmd.Append(' ').Append(Quote(a));
            if (!gui) cmd.Append(" -Elevated");      // konsol oynasi yopilib ketmasligi uchun "Enter" so'raydi

            string ps = Path.Combine(Environment.SystemDirectory, @"WindowsPowerShell\v1.0\powershell.exe");
            ProcessStartInfo psi = new ProcessStartInfo(ps, cmd.ToString());
            psi.UseShellExecute = false;
            psi.CreateNoWindow = gui;
            psi.WorkingDirectory = dir;

            using (Process p = Process.Start(psi))
            {
                p.WaitForExit();
                return p.ExitCode;
            }
        }
        catch (Exception ex)
        {
            MessageBox.Show("O'rnatuvchi ishga tushmadi:\n\n" + ex.Message, "Uzbek keyboard setup",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
        finally
        {
            try { if (Directory.Exists(dir)) Directory.Delete(dir, true); } catch { }
        }
    }
}
