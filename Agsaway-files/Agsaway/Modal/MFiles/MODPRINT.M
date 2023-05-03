if area_displayed == 1,
  [fprintname,printpthname] = uiputfile('*.ps','Printout File',0,0);
  if (fprintname ~= zeros(size(fprintname))),
    orient landscape;
    print (sprintf('%s',[printpthname fprintname]));
  end;
else
  modprint_err = errordlg('Must display an area first','PRINT ERROR');
end;