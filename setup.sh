pushd ../CTFd/
git diff CTFd/config.py > /tmp/diff
git clean -f
git reset --hard
git apply /tmp/diff
popd
cp -r * ../CTFd/CTFd/.
