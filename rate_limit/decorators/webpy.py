def rate_limit(LIMIT, WEB, max, duration):
    """
    simple decorator for use in webpy
    """
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            name = args[0].__class__.__name__ + '.' + f.__name__
            rate_ok = False
            try:
                result = LIMIT.checkRate(
                    name=name,
                    max=max,
                    duration=duration
                )

                #add rate headers
                WEB.header('X-RateLimit-Limit', max)
                WEB.header('X-RateLimit-Remaining', max - result.count)
                WEB.header('X-RateLimit-Reset', result.reset)

                #set HTTP code if limit is exceeded
                if not result.ok:
                    WEB.TooManyRequests()
            except:
                #Don't fail requests if limiting is broke
                rate_ok = True
                pass
            finally:
                if rate_ok:
                    return f(*args, **kwargs)
        return wrapped_f
    return wrap