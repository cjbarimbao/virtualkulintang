function varargout = voladjust_cont(varargin)
% VOLADJUST_CONT M-file for voladjust_cont.fig
%      VOLADJUST_CONT, by itself, creates a new VOLADJUST_CONT or raises the existing
%      singleton*.
%
%      H = VOLADJUST_CONT returns the handle to a new VOLADJUST_CONT or the handle to
%      the existing singleton*.
%
%      VOLADJUST_CONT('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in VOLADJUST_CONT.M with the given input arguments.
%
%      VOLADJUST_CONT('Property','Value',...) creates a new VOLADJUST_CONT or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before voladjust_cont_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to voladjust_cont_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help voladjust_cont

% Last Modified by GUIDE v2.5 02-Mar-2005 20:31:11

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @voladjust_cont_OpeningFcn, ...
                   'gui_OutputFcn',  @voladjust_cont_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
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


% --- Executes just before voladjust_cont is made visible.
function voladjust_cont_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to voladjust_cont (see VARARGIN)

% Choose default command line output for voladjust_cont
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
movegui(gcf, 'center');

% UIWAIT makes voladjust_cont wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = voladjust_cont_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background, change
%       'usewhitebg' to 0 to use default.  See ISPC and COMPUTER.
usewhitebg = 1;
if usewhitebg
    set(hObject,'BackgroundColor',[.9 .9 .9]);
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end


% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global VolGain;
VolGain = get(hObject,'Value')
[snd,Fs] = audioread('C:\Users\CJ\Desktop\198\Agsaway-files\Agsaway\FrankECE198\KulLTs\TestSet1\sample.wav');
sound(VolGain*snd,Fs);



% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
close(gcf);
uiresume;

