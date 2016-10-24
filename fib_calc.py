"""Calculate best path for FIB.

If something is the best path, return True for old False for new.
Return None if could not be determined.

Based on http://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html#bestpath

Lisa Roach
"""


def cmp_weight(new, old):
    """Compares the weights of the old link and the new link.
    Returns True if new > old, False if old > new, and None if they are equal.
    Default weight is 0, highest weight is preferred.

    >>> cmp_weight(100, 0)
    True
    >>> cmp_weight(0, 100)
    False
    >>> cmp_weight(0, 0)
    None
    """
    if new != old:
        return new > old
    else:
        return None

def cmp_local_pref(new, old):
    """Compares the local preference of the old link and the new link.
    Returns True if new > old, False if old > new, and None if they are equal.
    Default local preference is 100, highest local preference is preferred.

    >>> cmp_local_pref(100, 0)
    True
    >>> cmp_local_pref(0, 100)
    False
    >>> cmp_local_pref(100, 100)
    None
    """
    if new != old:
        return new > old
    else:
        return None

def locally_originated(old):
#locally originated - will these routes be added to a different table by default? -- No new paths will be locally originated.
#If a path is local we need to check if it is better based on 1 and 2 and stop there.
# Do they have a priority or weight associate with them?
    '''[{'metrics': {}, 'oif': 3, 'type': 1, 'dst_len': 24, 'family': 2, 'proto': 2, 'tos': 0, 'dst': '192.168.128.0/24', 'ipdb_priority': 0, 'priority': 600, 'flags': 0, 'encap': {}, 'src_len': 0, 'table': 254, 'multipath': [], 'prefsrc': '192.168.128.21', 'scope': 253, 'ipdb_scope': 'system'},
     {'metrics': {}, 'oif': 3, 'dst_len': 0, 'family': 2, 'proto': 4, 'tos': 0, 'dst': 'default', 'flags': 0, 'ipdb_priority': 0, 'priority': 600, 'scope': 0, 'encap': {}, 'src_len': 0, 'table': 254, 'multipath': [], 'type': 1, 'gateway': '192.168.128.1', 'ipdb_scope': 'system'},
     {'metrics': {}, 'oif': 3, 'dst_len': 16, 'family': 2, 'proto': 3, 'tos': 0, 'dst': '169.254.0.0/16', 'ipdb_priority': 0, 'priority': 1000, 'flags': 0, 'encap': {}, 'src_len': 0, 'table': 254, 'multipath': [], 'type': 1, 'scope': 253, 'ipdb_scope': 'system'}]
    '''

def cmp_AS_path(new, old):
#Compare AS Path. Shortest preferred. (kind of # of hops, so basically IPDB weight)
'''

   Network          Next Hop            Metric LocPrf Weight Path
*> 192.168.1.0      34.1.1.1                               0 300 100 10 i
*> 192.168.2.0      34.1.1.1                               0 300 100 10 i
'''
def cmp_origin(new, old):
# Compare Origin. Lowest preferred. IGP < EGP < INCOMPLETE

# Compare MED. Lowest preferred, only done if the AS path is identical.If the first hop AS is different or the MED is identical, move on to step 7.

def cmp_med(new, old):
    """Compares the MED of the old link and the new link.
    Returns True if new > old, False if old > new, and None if they are equal.
    Lowest MED is preferred, it is possible to have no MED.

    >>> cmp_med(100, 0)
    True
    >>> cmp_med(0, 100)
    False
    >>> cmp_med(100, 100)
    None
    """
    if new != old:
        return new > old
    else:
        return None
# 7. Compare neighbor type. eBGP preferred over iBGP. If best path selected here, move on to 9.
# 8. IGP Metric. Loest preferred.
# 9. Are multiple paths allowed
# etc
# etc
