pushd lkade-front
npm run build
popd
xcopy .\lkade-front\dist .\lkade-backend\vdist  /Y /S /I
pause
