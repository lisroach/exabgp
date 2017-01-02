from pyroute2 import IPDB

from exabgp.bgp.message import OUT

class FIB(object):
    def __init__(self):
        self.ipdb = IPDB() #Is this grabbing the cache for me?

class Store(FIB):

    def __init__(self, change):
        super(Store.__init__()) #I forget how to do this
        self.dst = change.nlri.prefix()
        self.nexthop = change.nlri.nexthop
        self.priority = change.attributes.values()[2] #we should be able to grab this with a key?
        self.action = change.nlri.action

    def update_fib(self):
        """Check if the route exists. If it does and it is an announcement,
        we check if the route needs to be updated.
        If it is a withdraw we remove route.
        If the route does not exist and is an announcement, we insert.
        """

        if self._route_exists():
            if self.action == OUT.ANNOUNCE:
                if self._best_path():
                    self._update_route()
            elif self.action == OUT.WITHDRAW:
                replacement_route = self._check_rib()
                if replacement_route:
                    self._update_route(replacement_route)
                self._remove_route()
                self.insert_route(replacement_route)
        else:
            self.insert_route()
        self.ipdb.release()

    def _route_exists(self):
        """Returns True if route exists in the FIB, False if not."""
        return {'dst': self.dst,
                'gateway': self.nexthop} in self.ipdb.routes

    def _best_path(self):
        """Calculates if new path is the better path."""
        pass

    def _check_rib(self):
        """Returns the next best path from the RIB if it exists."""
        pass

    def update_needed(self):
        pass

    def _update_route(self):
        pass

    def insert_route(self):
        """Insert the route in the FIB.
        We shouldn't have to keep our own cache, cause IPDB does that for us.
        If it already exists in cache identically, ignore.
        If it exists in cache but slightly different, update it.
        If it does not exist in cache, check the FIB.
        If it exists in FIB but slightly different, update it.
        If it is identical to what is in FIB, ignore it."""
        #nlri = [200.20.0.0/24 next-hop 10.0.0.11]
        self.ipdb.routes.add(dst=self.dst,
                             gateway=self.nexthop,
                             priority=self.priority
                        ).commit()
        #Not sure if we can caluculate MTU or advmss (metrics)
        #change.attrbutes is as follows:
        #origin igp local-preference 100
        #so possibly local-preference can be calculated

    def _remove_route(self):
        """Remove the route from the FIB."""
        with self.ipdb.routes[{'dst': self.dst,
                               'gateway': self.nexthop}] as route:
            route.remove()
        #Now we need to check if another route is in the RIB table
        #And if so, find the best path and add it to the fib.
