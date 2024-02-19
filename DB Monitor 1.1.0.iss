#define MyAppName "DB Monitor"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "God Forever"
#define MyAppExeName "DB Monitor.exe"

[Setup]
AppId={{CB9CB0B6-CF6B-4CFA-85E5-9816539CBC0F}}
UsePreviousAppDir=no
UsePreviousGroup=no
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:/Program Files/DB Monitor
DefaultGroupName={#MyAppName}
AllowNoIcons=no
OutputDir=..\DB Monitor 1.1.0\setup
OutputBaseFilename=DB Monitor 1.1.0
SetupIconFile=f:\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "f:\dist\DB Monitor 1.1.0\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "f:\dist\DB Monitor 1.1.0\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall"; Filename: "{app}\unins000.exe"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Registry]
Root: HKA; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "DB_Monitor"; ValueData: """{app}\DB Monitor.exe"" --hide"; Flags: uninsdeletevalue

[Code]
var
  myPage:TWizardPage;
  chk1,chk2:TNewRadioButton;
  fileName,setting:String;
  svArray: TArrayOfString;
procedure ClickCHK1(Sender:TObject);
begin
  setting:='{"delta": -180, "multi": 1.4, "roll": 40, "limit": 60, "warning": 100}' ;
end;
procedure ClickCHK2(Sender:TObject);
begin
  setting:='{"delta": -235, "multi": 1.6, "roll": 40, "limit": 60, "warning": 100}' ;
end;
procedure InitializeWizard();
begin
  myPage:=CreateCustomPage(wpWelcome, 'Select your Operating System', 'What is your current operating system?');
  chk1:=TNewRadioButton.Create(myPage);
  chk1.Parent:=myPage.Surface;
  chk1.Caption:='Windows 7';
  chk1.top:=20;
  chk1.OnClick:=@ClickCHK1;
  chk2:=TNewRadioButton.Create(myPage);
  chk2.Parent:=myPage.Surface;
  chk2.Caption:='Windows 10';
  chk2.top:=chk1.Top+20;
  chk2.OnClick:=@ClickCHK2;
  chk2.Checked := true;
end;
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep=ssPostinstall then 
  begin
    fileName := ExpandConstant('{app}\setting.json');
    LoadStringsFromFile(fileName, svArray);
    svArray[0]:=setting;
    SaveStringsToFile(fileName, svArray, false);
  end
end;

