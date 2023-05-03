function varargout = KulMenu(varargin)
% KULMENU M-file for KulMenu.fig
%      KULMENU, by itself, creates a new KULMENU or raises the existing
%      singleton*.
%
%      H = KULMENU returns the handle to a new KULMENU or the handle to
%      the existing singleton*.
%
%      KULMENU('Property','Value',...) creates a new KULMENU using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to KulMenu_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      KULMENU('CALLBACK') and KULMENU('CALLBACK',hObject,...) call the
%      local function named CALLBACK in KULMENU.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help KulMenu

% Last Modified by GUIDE v2.5 10-Feb-2005 21:10:23

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @KulMenu_OpeningFcn, ...
                   'gui_OutputFcn',  @KulMenu_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin & isstr(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

% End initialization code - DO NOT EDIT

% --- Executes just before KulMenu is made visible.
function KulMenu_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for KulMenu
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
movegui(gcf, 'center');

% UIWAIT makes KulMenu wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = KulMenu_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end


function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes on button press in radiobutton9.
function radiobutton9_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton9
set(handles.radiobutton10,'Value',0);
set(handles.radiobutton11,'Value',0);
set(handles.radiobutton12,'Value',0);
set(handles.radiobutton13,'Value',0);

% --- Executes on button press in radiobutton10.
function radiobutton10_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton10
set(handles.radiobutton9,'Value',0);
set(handles.radiobutton11,'Value',0);
set(handles.radiobutton12,'Value',0);
set(handles.radiobutton13,'Value',0);

% --- Executes on button press in radiobutton11.
function radiobutton11_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton11
set(handles.radiobutton10,'Value',0);
set(handles.radiobutton9,'Value',0);
set(handles.radiobutton12,'Value',0);
set(handles.radiobutton13,'Value',0);


% --- Executes on button press in radiobutton12.
function radiobutton12_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton12
set(handles.radiobutton10,'Value',0);
set(handles.radiobutton11,'Value',0);
set(handles.radiobutton9,'Value',0);
set(handles.radiobutton13,'Value',0);


% --- Executes on button press in radiobutton13.
function radiobutton13_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton13
set(handles.radiobutton10,'Value',0);
set(handles.radiobutton11,'Value',0);
set(handles.radiobutton12,'Value',0);
set(handles.radiobutton9,'Value',0);

% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global n11s n22s VolGain;
Volgain = 1;

instrument = [];
if get(handles.radiobutton9, 'Value')
    instrument = 'Agong';
end
if get(handles.radiobutton10, 'Value')
    instrument = 'Babandir'; 
end
if get(handles.radiobutton11, 'Value')
    instrument = 'Dabakan';
end
if get(handles.radiobutton12, 'Value')
    instrument = 'Gandingan';
end
if get(handles.radiobutton13, 'Value')
    instrument = 'Kulintang';
end
if isempty(instrument)
    p = guihandles(prompt);
    set(p.text1, 'string', 'Please select an instrument.');     % prompt fill instrument field
    uiwait;
    return;
end
if isempty(get(handles.edit1, 'string'))
    p = guihandles(prompt);
    set(p.text1, 'string', 'Please enter your name.');          % prompt fill name field
    uiwait;
    return;
end

name = get(handles.edit1,'String');
filedir= 'C:\FrankECE198\KulLTs\TestSet\TestResults\';
testdir = 'C:\FrankECE198\KulLTs\TestSet\';
FID = fopen(sprintf('%s%s_%s.txt', filedir, name, lower(instrument)),'w');
close(gcf);

ins = lower(instrument(1));
switch(ins)                     % number of styles: n/2 per instrument, factor of 2 due to order (O-S or S-O)
    case {'a'}
        n = 12; maxrep = 6;
    case {'b'}
        n = 8; maxrep = 8;
    case {'d'}
        n = 6; maxrep = 10;
    case {'g'}
        n = 16; maxrep = 4;
    case {'k'}
        n = 4; maxrep = 16;
end

n11s = zeros(1, n/2);
n22s = zeros(1, n/2);

g = guihandles(kulsynthLT);
movegui(gcf,'center');
set(g.text3, 'string', instrument);
set(g.text4, 'string', 'Listening Test 1');

sample = wavread(sprintf('%s%s1o', testdir, ins));
wavwrite(sample, 44100, 16, sprintf('%ssample', testdir));

waitfor(voladjust_cont);
ListeningTest(1, g, ins, n, maxrep);
n11_lt1 = sum(n11s);
n22_lt1 = sum(n22s);

set(g.text4, 'string', 'Listening Test 2');
set(g.text5, 'string', '');
p = guihandles(prompt);
set(p.figure1, 'Name', 'Listening Test 2');
set(p.text1, 'String', 'That ends Listening Test 1 of 3. You may now take a short BREAK.');
set(p.pushbutton1, 'string', 'Continue to Listening Test 2');
set(p.pushbutton1, 'FontWeight', 'bold');
uiwait;
ListeningTest(2, g, ins, n, maxrep);
n11_lt2 = sum(n11s) - n11_lt1;
n22_lt2 = sum(n22s) - n22_lt1;

set(g.text4, 'string', 'Listening Test 3');
set(g.text5, 'string', '');
p = guihandles(prompt);
set(p.figure1, 'Name', 'Listening Test 3');
set(p.text1, 'String', 'That ends Listening Test 2 of 3. You may now take a short BREAK.');
set(p.pushbutton1, 'string', 'Continue to Listening Test 3');
set(p.pushbutton1, 'FontWeight', 'bold');
uiwait;
ListeningTest(3, g, ins, 2*n, ceil(maxrep/2));
n11_lt3 = sum(n11s) - n11_lt1 - n11_lt2;
n22_lt3 = sum(n22s) - n22_lt1 - n22_lt2;

p = guihandles(prompt);
set(p.figure1, 'Name', 'Thank You');
set(p.text1, 'String', 'That ends our Listening Test. THANK YOU!');
set(p.text1, 'FontWeight', 'bold');
set(p.pushbutton1, 'string', 'OK');
uiwait;


n11 = sum(n11s);
n22 = sum(n22s);
fprintf(FID, '%d %d\n%d %d\n%d %d\n\n', n11_lt1, n22_lt1, n11_lt2, n22_lt2, n11_lt3, n22_lt3);
for i = 1:length(n11s)
    fprintf(FID, '%d %d\n', n11s(i), n22s(i));
end
fprintf(FID, '\n%d %d \n%d %d', n11, n22, 3*maxrep*n/2, 3*maxrep*n/2);
fprintf(FID, '\n\nFormat: [n11 per LT n22 per LT];[n11 per style n22 per style];[n11 n22]; [n1 n2]');
fprintf(FID, '\nn11 = number of times O-S was chosen when O-S was presented');
fprintf(FID, '\nn22 = number of times S-O was chosen when S-O was presented');
fprintf(FID, '\nn1 = number of times that ORIG followed by SYNTH (O-S) was presented');
fprintf(FID, '\nn2 = number of times that SYNTH followed by ORIG (S-O) was presented');
clockvec = clock;
fprintf(FID, sprintf('\n\nDate created: %.2d-%.2d-%d %.2d:%.2d.%.2d', clockvec(1:end-1), round(clockvec(end))) );
fclose(FID);
close(gcf);
disp(sprintf('\n\n\n\t\t\tThank You\n\t\t\tTapos na ang Listening Test :)\n\n\n'));

%-----Main Listening Test
function ListeningTest(ltnum, g, ins, n, maxrep)

global B1 B2 VolGain n11s n22s;

playstyle = [];
for i = 1:maxrep
    playstyle = [playstyle randperm(n)];
end

len = n*maxrep;
playorder = zeros(1, len);
playvol1 = ones(1, len);
playvol2 = ones(1, len);
rev = find(playstyle > n/2);
playorder(rev) = 1;
playstyle(rev) = playstyle(rev) - n/2;

if ltnum == 3
    lessint2 = find(playstyle <= n/4);
    playvol2(lessint2) = playvol2(lessint2)/2;
    lessint1 = find(playstyle > n/4);
    playvol1(lessint1) = playvol1(lessint1)/2;
    playstyle(lessint1) = playstyle(lessint1) - n/4;
end    

set(g.text4, 'string', sprintf('Listening Test %d', ltnum));
col1 = get(g.frame2, 'BackgroundColor');
col2 = [0 0.7 0.3];
testdir = 'C:\FrankECE198\KulLTs\TestSet\';
for i = 1:len
    [orig,Fs] = wavread(sprintf('%s%s%do', testdir, ins, playstyle(i)));
    [synth] = wavread(sprintf('%s%s%ds', testdir, ins, playstyle(i)));
    nosound = zeros(0.05*Fs,2); 
    
    if ~playorder(i)
        int1 = playvol1(i)*[orig;nosound];
        int2 = playvol2(i)*[nosound;synth];
    else
        int1 = playvol1(i)*[synth;nosound];
        int2 = playvol2(i)*[nosound;orig];       
    end
    
    set(g.text5, 'string', 'Ready');
    set(g.frame6, 'BackgroundColor', [0.8 0 0]);
    set(g.text5, 'BackgroundColor', [0.8 0 0]);
    set(g.text5, 'ForegroundColor', [1 1 1]);
    pause(0.5);
    set(g.text5, 'ForegroundColor', [0.925 0.302 0]);
    set(g.text5, 'BackgroundColor', [0.902 0.902 0.902]);
    set(g.frame6, 'BackgroundColor', [0.902 0.902 0.902]);
    set(g.text5, 'string', 'Ready');
    pause(0.5);
    set(g.text5, 'string', 'Ready');
    set(g.frame6, 'BackgroundColor', [0.8 0 0]);
    set(g.text5, 'BackgroundColor', [0.8 0 0]);
    set(g.text5, 'ForegroundColor', [1 1 1]);
    pause(1);
    set(g.text5, 'ForegroundColor', [0.925 0.302 0]);
    set(g.text5, 'BackgroundColor', [0.902 0.902 0.902]);
    set(g.frame6, 'BackgroundColor', [0.902 0.902 0.902]);
    set(g.text5, 'string', 'Ready');
    pause(1);
    
    set(g.text5, 'string', sprintf('Interval Pair %d of %d', i, len));
    pause(2);
 
    
%     p = guihandles(prompt);
%     set(p.figure1, 'Name', 'Next Signal');
%     set(p.text1, 'String', 'Ready');  
%     set(p.text1,'FontWeight', 'bold');  
%     set(p.pushbutton1, 'string', 'OK');
%     set(p.pushbutton1, 'FontWeight', 'bold');
%     uiwait;
    
    set(g.text7, 'FontWeight', 'bold');
    set(g.frame2, 'backgroundColor', col2);
    set(g.text7, 'backgroundColor', col2);
    
    sound(VolGain*int1, Fs);
    pause(size(int1,1)/Fs);
 
    set(g.text7, 'FontWeight', 'normal');
    set(g.frame2, 'backgroundColor', col1);
    set(g.text7, 'backgroundColor', col1);
    
    set(g.text8, 'FontWeight', 'bold');
    set(g.frame4, 'backgroundColor', col2);
    set(g.text8, 'backgroundColor', col2);
    
    sound(VolGain*int2, Fs);
    pause(size(int1,1)/Fs);
    
    set(g.text8, 'FontWeight', 'normal');
    set(g.frame4, 'backgroundColor', col1);
    set(g.text8, 'backgroundColor', col1);
    
    uiwait
    
    
    if (~playorder(i) & B1) | (playorder(i) & B2)
        if ~playorder(i)
            n11s(playstyle(i)) = n11s(playstyle(i)) + 1;
        else
            n22s(playstyle(i)) = n22s(playstyle(i)) + 1;
        end
            
        if i < 4
            p = guihandles(prompt);
            set(p.text1, 'FontWeight', 'bold');
            set(p.text1, 'string', 'You are CORRECT.');
            uiwait;
        end
    else
        if i < 4
            p = guihandles(prompt);
            set(p.text1, 'FontWeight', 'bold');
            set(p.text1, 'string', 'You are INCORRECT.');
            uiwait;
        end
    end
     
end



% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global B1 B2
B1 = 1;
B2 = 0;
uiresume;


% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global B1 B2
B1 = 0;
B2 = 1;
uiresume;