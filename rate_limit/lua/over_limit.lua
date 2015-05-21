--load globals to local for performance
local redis = redis
local tonumber = tonumber

--params
local max = tonumber(ARGV[1])
local duration = tonumber(ARGV[2])
local keyname = KEYS[1]..':'..duration --only support a single key

--Helper to calculate reset time
local function getResetEpoch(ttl)
    local now = redis.call("TIME")
    return now[1] + ttl
end

--main rate check logic
local current = redis.call("GET", keyname)
if not current then
    local current = redis.call("INCR", keyname)
    redis.call("EXPIRE", keyname, duration)
    return {true, current, getResetEpoch(duration)}
else
    local ttl = redis.call("TTL", keyname)
    if ttl == -1 then
        --catch leaky keys where expiration was never created
        ttl = duration
        redis.call("EXPIRE", keyname, ttl)
    end

    local total_weight = current + 1;
    if total_weight > max then
        return {false, current, getResetEpoch(ttl)}
    else
        local current = redis.call("INCR", keyname)
        return {true, current, getResetEpoch(ttl)}
    end
end


