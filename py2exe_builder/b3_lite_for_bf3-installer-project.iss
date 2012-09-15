; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

;#define Debug
#define B3_VERSION_NUMBER "1.9.0"
#define B3_VERSION_SUFFIX "dev4"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
;AppId={{F04D6FC4-CF46-4409-995A-04BEB0B219E6}
AppID=5FB180C6-A3B3-46CF-85E0-F00168F1569C
AppName=BigBrotherBot lite for Battlefield 3
AppVerName=BigBrotherBot {#B3_VERSION_NUMBER}{#B3_VERSION_SUFFIX}
AppPublisher=BigBrotherBot
AppPublisherURL=http://www.bigbrotherbot.net/
AppSupportURL=http://www.bigbrotherbot.net/
AppUpdatesURL=http://www.bigbrotherbot.net/
AppCopyright=Copyright (C) 2005-2011 BigBrotherBot.net
DefaultDirName={sd}\BigBrotherBot
DefaultGroupName=BigBrotherBot
LicenseFile=assets_common\gpl-2.0.txt
OutputBaseFilename=BigBrotherBot_lite_bf3-{#B3_VERSION_NUMBER}{#B3_VERSION_SUFFIX}-win32
#ifndef Debug
Compression=lzma/Ultra64
SolidCompression=true
InternalCompressLevel=Normal
#else
Compression=none
SolidCompression=false
InternalCompressLevel=none
#endif
DisableStartupPrompt=true
SetupLogging=true
VersionInfoVersion=1.0
VersionInfoDescription=B3 lite for BF3 installation
VersionInfoCopyright=www.bigbrotherbot.net
VersionInfoTextVersion=1.0
VersionInfoProductName=BigBrotherBot
VersionInfoProductVersion={#B3_VERSION_NUMBER}
ExtraDiskSpaceRequired=11790316
RestartIfNeededByRun=false
PrivilegesRequired=none
WizardImageBackColor=clBlack
WindowVisible=false
BackColor=clBlack
BackColor2=clGray
WizardSmallImageFile=assets_common\WizB3SmallImage.bmp
WizardImageFile=assets_b3_lite_for_bf3\WizB3Image.bmp
UsePreviousAppDir=true
AlwaysShowDirOnReadyPage=true
AlwaysShowGroupOnReadyPage=true
VersionInfoCompany=BigBrotherBot.net
WindowShowCaption=false
WindowResizable=false
SetupIconFile=assets_common\b3.ico
EnableDirDoesntExistWarning=false
DirExistsWarning=yes
DisableProgramGroupPage=auto

[Languages]
Name: english; MessagesFile: compiler:Default.isl
Name: basque; MessagesFile: compiler:Languages\Basque.isl
Name: brazilianportuguese; MessagesFile: compiler:Languages\BrazilianPortuguese.isl
Name: catalan; MessagesFile: compiler:Languages\Catalan.isl
Name: czech; MessagesFile: compiler:Languages\Czech.isl
Name: danish; MessagesFile: compiler:Languages\Danish.isl
Name: dutch; MessagesFile: compiler:Languages\Dutch.isl
Name: finnish; MessagesFile: compiler:Languages\Finnish.isl
Name: french; MessagesFile: compiler:Languages\French.isl
Name: german; MessagesFile: compiler:Languages\German.isl
Name: hebrew; MessagesFile: compiler:Languages\Hebrew.isl
Name: hungarian; MessagesFile: compiler:Languages\Hungarian.isl
Name: italian; MessagesFile: compiler:Languages\Italian.isl
Name: norwegian; MessagesFile: compiler:Languages\Norwegian.isl
Name: polish; MessagesFile: compiler:Languages\Polish.isl
Name: portuguese; MessagesFile: compiler:Languages\Portuguese.isl
Name: russian; MessagesFile: compiler:Languages\Russian.isl
Name: slovak; MessagesFile: compiler:Languages\Slovak.isl
Name: slovenian; MessagesFile: compiler:Languages\Slovenian.isl
Name: spanish; MessagesFile: compiler:Languages\Spanish.isl

[Icons]
Name: {group}\{cm:executable,b3_run}; Filename: {app}\b3_run.exe; Parameters: "--config ""{app}\conf\b3.xml"""; WorkingDir: {app}; Flags: dontcloseonexit; IconFilename: {app}\b3.ico; Comment: "Run BigBrotherBot {#B3_VERSION_NUMBER}{#B3_VERSION_SUFFIX}"; 
Name: {commondesktop}\{cm:executable,b3_run}; Filename: {app}\b3_run.exe; Parameters: "--config ""{app}\conf\b3.xml"""; WorkingDir: {app}; Flags: dontcloseonexit; IconFilename: {app}\b3.ico; Comment: "Run BigBrotherBot {#B3_VERSION_NUMBER}{#B3_VERSION_SUFFIX}"; 
Name: {group}\{cm:configWizard,Config wizard}; Filename: {app}\b3_run.exe; Parameters: "--config ""{app}\conf\b3.xml"" --setup"; WorkingDir: {app}; Comment: "Run the B3 setup wizard"; Flags: dontcloseonexit; 
Name: {group}\{cm:updateWizard,Database update}; Filename: {app}\b3_run.exe; Parameters: "--config ""{app}\conf\b3.xml"" --update"; WorkingDir: {app}; Comment: "Run the B3 update wizard"; Flags: dontcloseonexit; 
Name: {group}\{cm:B3ConfDir,config}; Filename: {app}\conf\
Name: {group}\{cm:extplugins,extplugins}; Filename: {app}\extplugins\; IconFilename: {app}\b3-plugins-icon.ico; 
Name: {group}\extra\{cm:docs,docs}; Filename: {app}\docs\
Name: {group}\extra\{cm:sql,sql}; Filename: {app}\sql\
Name: {group}\{cm:UninstallProgram,BigBrotherBot}; Filename: {uninstallexe}
Name: {group}\web\{cm:Website,BigBrotherBot}; Filename: http://www.bigbrotherbot.net/
Name: {group}\web\{cm:Manual,Manual}; Filename: http://wiki.github.com/BigBrotherBot/big-brother-bot/manual
Name: {group}\web\{cm:Forums,B3 Forums}; Filename: http://forum.bigbrotherbot.net/
Name: {group}\web\{cm:DownloadPlugins,Download plugins}; Filename: http://forum.bigbrotherbot.net/downloads/?cat=4
Name: {group}\web\{cm:B3configGenerator,B3 config generator}; Filename: http://config.bigbrotherbot.net/; 
Name: {group}\web\artwork; Filename: http://www.bigbrotherbot.net/logos
Name: {group}\web\other tools\{cm:Echelon,Echelon}; Filename: http://echelon.bigbrotherbot.net/

;[Dirs]
Name: {group}\web\other tools\{cm:Xlrstats,XLRstats}; Filename: http://www.xlrstats.com/

[Files]
Source: "{app}\conf\*"; DestDir: "{app}\conf\backup"; Flags: external skipifsourcedoesntexist uninsneveruninstall
Source: "assets_common\readme-windows.txt"; DestDir: "{app}"
Source: "dist_py2exe\b3_run.exe"; DestDir: "{app}"
Source: "dist_py2exe\b3.lib"; DestDir: "{app}"
Source: "dist_py2exe\PKG-INFO"; DestDir: "{app}"
Source: "dist_py2exe\README.md"; DestDir: "{app}"
Source: "dist_py2exe\docs\*"; DestDir: "{app}\docs"; Flags: recursesubdirs
Source: "dist_py2exe\sql\*"; DestDir: "{app}\sql"; Flags: recursesubdirs
Source: "dist_py2exe\extplugins\*"; DestDir: "{app}\extplugins"; Flags: recursesubdirs
Source: "assets_b3_lite_for_bf3\extplugins\*"; DestDir: "{app}\extplugins"; Flags: recursesubdirs
Source: "dist_py2exe\conf\*"; DestDir: "{app}\conf"; Flags: recursesubdirs
Source: "assets_b3_lite_for_bf3\conf\*"; DestDir: {app}\conf; Flags: recursesubdirs;
Source: "assets_common\b3.ico"; DestDir: "{app}"
Source: "assets_common\b3-plugins-icon.ico"; DestDir: "{app}"
Source: "assets_b3_lite_for_bf3\sed.exe"; DestDir: "{tmp}"; Flags: dontcopy
Source: "assets_b3_lite_for_bf3\makeB3DotXml.bat"; DestDir: "{tmp}"; Flags: dontcopy
Source: "assets_b3_lite_for_bf3\frostbite_server_info.exe"; DestDir: "{tmp}"; Flags: dontcopy
Source: "assets_b3_lite_for_bf3\frostbite_server_info.bat"; DestDir: "{tmp}"; Flags: dontcopy
Source: "assets_b3_lite_for_bf3\template_b3.xml"; DestDir: "{tmp}"; Flags: dontcopy
Source: {tmp}\b3.xml; DestDir: {app}\conf; Flags: external; 


[UninstallDelete]
Name: {app}\*; Type: filesandordirs

[CustomMessages]
Website=BigBrotherBot Website
Forums=Forums
Manual=Manual
B3ConfDir=config folder
extplugins=plugins folder
configWizard=Run B3 config wizard
updateWizard=Update B3 database
executable=Run B3
DownloadPlugins=Download more plugins
Echelon=Echelon
Xlrstats=XLRstats
B3configGenerator=B3 config generator
sql=sql folder
docs=docs folder

[Run]
Filename: {app}\readme.txt; Flags: ShellExec SkipIfDoesntExist;
Filename: {app}\b3_run.exe; Parameters: "--config ""{app}\conf\b3.xml"""; WorkingDir: {app}; Flags: ShellExec PostInstall; Description: "Run B3"; BeforeInstall: ExplainIamGod; 

[Code]
var
  RconPage: TInputQueryWizardPage;
  RconIp, RconPassword: String;
  RconPort: integer;



procedure MakeB3XmlFile();
var
  ResultCode: Integer;
  ProgramParams: String;
begin
  ProgramParams := RconIp + ' ' + IntToStr(RconPort) + ' ' + RconPassword;
  Log('exec : ' + ExpandConstant('{tmp}\makeB3DotXml.bat') + ' ' + ProgramParams);
  if not Exec(ExpandConstant('{tmp}\makeB3DotXml.bat'), ProgramParams, '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then begin
     MsgBox('Failed to create b3.xml' + #13#13 + SysErrorMessage(ResultCode), mbError, MB_OK);
     Abort();
  end;
  // NOTE : {tmp}\b3.xml will be copied will all other files as part of the normal
  //        file copy step.
end;

procedure RegisterPreviousData(PreviousDataKey: Integer);
begin
  { Store the settings so we can restore them next time }
  SetPreviousData(PreviousDataKey, 'RconIp', RconPage.Values[0]);
  SetPreviousData(PreviousDataKey, 'RconPort', RconPage.Values[1]);
end;

function TestFrostbiteConnection(): Boolean;
var
  ResultCode: Integer;
  ProgramParams: String;
  ServerInfoFilePath: String;
  PasswordAccepted: String;
begin
  ServerInfoFilePath := ExpandConstant('{tmp}\frostbite_server_info.ini');
  ProgramParams := RconIp + ' ' + IntToStr(RconPort) + ' --password=' + RconPassword + ' --timeout=3 --format=ini';
  Log('exec : ' + ExpandConstant('{tmp}\frostbite_server_info.bat') + ' ' + ProgramParams);
  Result := FALSE;
  if not Exec(ExpandConstant('{tmp}\frostbite_server_info.bat'), ProgramParams, '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then begin
     MsgBox('TestFrostbiteConnection:' + #13#13 + 'Execution of ''frostbite_server_info.exe ' +  ProgramParams + ''' failed. ' + SysErrorMessage(ResultCode) + '.', mbError, MB_OK);
  end else begin
    PasswordAccepted := GetIniString('general', 'password_accepted', '', ServerInfoFilePath);
    Log('PasswordAccepted: ' + PasswordAccepted);
    if CompareStr(PasswordAccepted, 'True') = 0 then begin
      Result := TRUE;
    end else begin
      if CompareStr(PasswordAccepted, 'False') = 0 then begin
        MsgBox('Error while checking server information' + #13#13 + 'Invalid Password' + #13#13 + GetIniString('general', 'error', '', ServerInfoFilePath), mbError, MB_OK);
      end else begin
        MsgBox('Error while checking server information' + #13#13 + GetIniString('general', 'error', '', ServerInfoFilePath) + #13#13 + 'Check that the IP address and port are correct and' + #13 + 'that your game server is running', mbError, MB_OK); 
      end;
    end;
  end;
end;


procedure ExplainIamGod();
begin
  MsgBox('Instructions to become super admin on your BF3 server' + #13#13 + 'After you close this message, B3 will start up.' 
    + #13 + 'Then join your game server and type "!iamgod" in the chat.' 
    + #13#13 + 'You should get a response from B3 telling you that you are now superadmin.'
    + #13 + 'Type "!help" to have a list of available commands.' 
    , mbInformation, MB_OK);  
end;



{ InnoSetup events handlers }

procedure InitializeWizard;
begin
  { Create the pages }
  
  // Create the page
  RconPage := CreateInputQueryPage(wpReady,
    'Battlefield 3 server information', 'Server configuration',
    'Please specify your Battlefield server IP address, RCON port and RCON password, then click Next.');
  
  RconPage.Add('Server IP:', False);
  RconPage.Add('RCON port:', False);
  RconPage.Add('RCON password:', False);
  
  { Set default values, using settings that were stored last time if possible }

  RconPage.Values[0] := GetPreviousData('RconIp', '');
  RconPage.Values[1] := GetPreviousData('RconPort', '');
  
  { extract files required for the installation }
  ExtractTemporaryFile('frostbite_server_info.exe');
  ExtractTemporaryFile('frostbite_server_info.bat');
  ExtractTemporaryFile('sed.exe');
  ExtractTemporaryFile('makeB3DotXml.bat');
  ExtractTemporaryFile('template_b3.xml');
end;


function ShouldSkipPage(PageID: Integer): Boolean;
begin
#ifdef Debug
  case PageID of
		wpWelcome :
		Result := TRUE;
		wpLicense :
		Result := TRUE;
		wpPassword :
		Result := TRUE;
		wpInfoBefore :
		Result := TRUE;
		wpUserInfo :
		Result := TRUE;
		wpSelectDir :
		Result := TRUE;
		wpSelectComponents :
		Result := TRUE;
		wpSelectProgramGroup :
		Result := TRUE;
		wpSelectTasks :
		Result := TRUE;
		wpReady :
		Result := TRUE;
		wpPreparing :
		Result := TRUE;
		wpInstalling :
		Result := FALSE;
		wpInfoAfter :
		Result := FALSE;
		wpFinished :
		Result := FALSE;
	else
		Result := FALSE;
	end;
#else
  Result := FALSE;
#endif 
end;


procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then begin
    MakeB3XmlFile();
  end;
end;



function NextButtonClick(CurPageID: Integer): Boolean;
begin
  { Validate certain pages before allowing the user to proceed }
  if CurPageID = RconPage.ID then begin
    if RconPage.Values[0] = '' then begin
      MsgBox('You must enter your server IP address.', mbError, MB_OK);
      Result := False;
    end else if RconPage.Values[1] = '' then begin
      MsgBox('You must enter your server RCON port.', mbError, MB_OK);
      Result := False;
    end else if RconPage.Values[2] = '' then begin
      MsgBox('You must enter your server RCON password.', mbError, MB_OK);
      Result := False;
    end else begin
      RconIp := RconPage.Values[0];
      RconPort := StrToInt(RconPage.Values[1]);
      RconPassword := RconPage.Values[2];
      Result := TestFrostbiteConnection();
    end;
  end else
    Result := True;
end;



