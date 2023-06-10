VENV_BIN=".venv/bin"

if ["$ENV_FOR_DYNACONF" != "testing"]; then
    echo "Warning ENV_FOR_DYNACONF is not set to testing: $ENV_FOR_DYNACONF"
fi

# Kill all previoust instances if there is one up
echo "killing all existing 'sam' processes running"
killall -KILL sam > /dev/null 2>&1 || true

echo "Start local lambda function ..."
. ${VENV_BIN}/activate && ENV_FOR_DYNACONF=testing sam local start-lambda > /dev/null 2>&1 &
sleep 5
echo "Function started"

echo "Testing http://127.0.0.1:3001 to see if it is running ..."
curl -s 'http://127.0.0.1:3001' || (echo "Error: function is not running." && exit 1)
echo "Function is up."