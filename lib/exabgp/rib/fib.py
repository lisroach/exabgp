from pyroute2 import IPDB
import redis

from exabgp.bgp.message import IN

class FIB(object):
    def __init__(self):
        self.ipdb = IPDB() #Is this grabbing the cache for me?
        self.redis = RedisStore()

    def update_fib(self, change):
        """Check if the route exists. If it does and it is an announcement,
        we check if the route needs to be updated.
        If it is a withdraw we remove route.
        If the route does not exist and is an announcement, we insert.
        """
        if self._route_exists(change):
            if change.nlri.action == IN.ANNOUNCED:
                if self._best_path(change):
                    self._update_route(change)
            elif change.nlri.action == IN.WITHDRAWN:
                replacement_route = self._check_rib(change)
                if replacement_route:
                    self._update_route(replacement_route)
                else:
                    self._remove_route(change)
        else:
            self._insert_route(change)
        self.ipdb.release()

    def _route_exists(self, change):
        """Returns True if route exists in the FIB, False if not."""
        return {'dst': change.nlri.prefix()} in self.ipdb.routes

    def _best_path(self):
        """Calculates if new path is the better path.
        True if new path is better. False if old path is better."""
        old_high_score = self.redis.get_high_score(self.dst)
        new_high_score = BGPScore(self.attributes)
        return old_high_score < new_high_score

    def _check_rib(self, change):
        """Returns the next best path from the RIB if it exists."""
        #Remove the highest score from the RIB.
        #Grab and return the next highest score.
        pass

    def _update_route(self, change):
        pass

    def _insert_route(self, change):
        """Insert the route in the FIB."""
        #nlri = [200.20.0.0/24 next-hop 10.0.0.11]
        self.ipdb.routes.add(self.route).commit()
        #Not sure if we can caluculate MTU or advmss (metrics)
        #change.attrbutes is as follows:
        #origin igp local-preference 100
        #so possibly local-preference can be calculated

    def _remove_route(self, change):
        """Remove the route from the FIB."""
        with self.ipdb.routes[self.route] as route:
            route.remove()

class RedisStore(object):
    """Keeps track of all seen routes and their 'rank' according to BGP best
    path."""
    def __init__(self, ip='127.0.0.1', port=6379, db=0):
        self.conn = redis.Redis(host=ip, port=port, db=db)
        self.count = 0

    def add_route(self, dst, nlri, score):
        """Add a route to Redis."""
        ok = self.conn.zadd(dst, nlri, score)
        if ok:
            self.count += 1

    def get_routes(self, dst, withscores=False):
        """Get all the routes for a destination."""
        self.conn.zrange(dst, 0, self.count, withscores=withscores)

    def get_high_score(self, dst):
        """Return the highest Redis score (the winning BGP path)."""
        return self.conn.zrange(dst, 0, 1, desc=True)

class BGPScore(object):
    """Calculate best path."""
    def __init__(self, attributes):
        pass




