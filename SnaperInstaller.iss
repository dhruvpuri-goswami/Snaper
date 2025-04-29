[Setup]
AppName=Snaper
AppVersion=1.0
AppPublisher=Dhruvpuri Goswami            
AppPublisherURL=https://github.com/dhruvpuri-goswami 
AppSupportURL=https://github.com/dhruvpuri-goswami/Snaper
AppUpdatesURL=https://github.com/dhruvpuri-goswami/Snaper/releases
AppCopyright=© 2025 Dhruvpuri Goswami 
DefaultDirName={pf}\Snaper
DefaultGroupName=Snaper
OutputBaseFilename=Snaper
Compression=lzma
SolidCompression=yes
SetupIconFile=snaper.ico


[Files]
Source: "InstallerBuild\Snaper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerBuild\Tesseract-OCR\*"; DestDir: "{app}\Tesseract-OCR"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Snaper"; Filename: "{app}\Snaper.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\snaper.ico"
Name: "{userdesktop}\Snaper"; Filename: "{app}\Snaper.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\snaper.ico"

[Run]
Filename: "{app}\Snaper.exe"; Description: "Launch Snaper"; Flags: nowait postinstall skipifsilent
