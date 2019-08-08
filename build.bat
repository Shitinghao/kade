pushd lkade-front
npm run build
popd
xcopy .\lkade-front\dist .\lkade-backend\dist  /Y /S /I
pause
