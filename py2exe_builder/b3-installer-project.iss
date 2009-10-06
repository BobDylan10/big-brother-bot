; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!


;#define Debug

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{F04D6FC4-CF46-4409-995A-04BEB0B219E6}
AppName=BigBrotherBot
AppVerName=BigBrotherBot 1.2.0b
AppPublisher=BigBrotherBot
AppPublisherURL=http://www.bigbrotherbot.com/
AppSupportURL=http://www.bigbrotherbot.com/forums/
AppUpdatesURL=http://www.bigbrotherbot.com/
DefaultDirName={pf}\BigBrotherBot_1.2.0b
DefaultGroupName=BigBrotherBot
LicenseFile=gpl-2.0.txt
OutputBaseFilename=BigBrotherBot-1.2.0b-win32
Compression=lzma/ultra64
SolidCompression=true
InternalCompressLevel=normal
DisableStartupPrompt=true
SetupLogging=true
VersionInfoVersion=1.0
VersionInfoDescription=B3 installation
VersionInfoCopyright=Courgette
AppCopyright=Copyright � 2005 Michael "ThorN" Thornton
VersionInfoTextVersion=1.0
VersionInfoProductName=BigBrotherBot
VersionInfoProductVersion=1.2.0b
ExtraDiskSpaceRequired=8950624
RestartIfNeededByRun=false
PrivilegesRequired=none
WizardImageBackColor=$804000

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
Name: {group}\{cm:executable,b3_run}; Filename: {app}\b3_run.exe; Parameters: -c {app}\conf\b3.xml; WorkingDir: {app}
Name: {group}\{cm:Website,BigBrotherBot}; Filename: http://www.bigbrotherbot.com/
Name: {group}\{cm:Forums,B3 Forums}; Filename: http://www.bigbrotherbot.com/forums/
Name: {group}\{cm:UninstallProgram,BigBrotherBot}; Filename: {uninstallexe}


[Files]
Source: ..\dist_py2exe\*; DestDir: {app}; Flags: recursesubdirs



[Components]


[UninstallDelete]
Name: {app}\*; Type: filesandordirs


[CustomMessages]
Website=BigBrotherBot Website
Forums=B3 Forums
B3ConfDir=B3 config
B3guide=B3 Guide
executable=Run B3
