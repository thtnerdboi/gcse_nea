set /p input= Type commit message
git add . 
git commit -m "%input%"
git push origin main
echo yay