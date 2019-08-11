pushd lkade-front
start npm run build
pause
popd
xcopy .\lkade-front\dist .\lkade-backend\vdist  /Y /S /I
pause
