function varargout = KulSynthLT(varargin)
% KULSYNTHLT M-file for KulSynthLT.fig
%      KULSYNTHLT, by itself, creates a new KULSYNTHLT or raises the existing
%      singleton*.
%
%      H = KULSYNTHLT returns the handle to a new KULSYNTHLT or the handle to
%      the existing singleton*.
%
%      KULSYNTHLT('Property','Value',...) creates a new KULSYNTHLT using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to KulSynthLT_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      KULSYNTHLT('CALLBACK') and KULSYNTHLT('CALLBACK',hObject,...) call the
%      local function named CALLBACK in KULSYNTHLT.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help KulSynthLT

% Last Modified by GUIDE v2.5 10-Feb-2005 21:56:59

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @KulSynthLT_OpeningFcn, ...
                   'gui_OutputFcn',  @KulSynthLT_OutputFcn, ...
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


% --- Executes just before KulSynthLT is made visible.
function KulSynthLT_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for KulSynthLT
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes KulSynthLT wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = KulSynthLT_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;