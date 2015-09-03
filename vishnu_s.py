"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections                                                                   
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
import os                                                               

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self, snum, hnum ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )
        swi = {}
        hos = {}
        # Add hosts and switches
        print "reached 1"
        snum = int(snum)
        hnum = int(hnum)
        #print type(snum)
        for x in xrange(snum):
            s = self.addSwitch("s" +str(x+1))
        #    print "added s" + str(x+1)
            swi[x+1]= s
        print "reached 2 "
        #print swi

        for x in xrange(hnum):
            h = self.addHost("h" +str(x+1))
            hos[x+1]= h
        print "reached 3"

        
        # Add links
        for x in xrange(snum):
            for y in xrange(x):
                self.addLink(swi[x+1],swi[y+1])
        print "reached 4"

        sph = hnum/snum
        sin = swi.keys()
        skey = sin*int(hnum/snum)
        print skey
        tmp = sin[:(hnum%snum)]
        print tmp
        skey = skey + tmp
        skey.sort()
        print skey
        i = 1
        for x in skey:
            self.addLink(swi[x], hos[i])
            i = i+1

def testTopo(snum,hnum):
    topo = MyTopo(snum, hnum)
    net = Mininet(topo, controller=RemoteController)
    net.start()
    net.addController('c0', controller=RemoteController,ip="127.0.0.1",port=6633)
    #print "hereeeeeeeeeeeeeee"
    #print net.keys()
    for x in xrange(hnum):
        for y in xrange(hnum):
            if x%2==0 and y%2==1:
                net.nameToNode["h"+str(x+1)].cmd("iptables -A OUTPUT -o h1-eth0 -d 10.0.0."+ str(y+1)+" -j DROP")
                net.nameToNode["h"+str(y+1)].cmd("iptables -A OUTPUT -o h1-eth0 -d 10.0.0."+ str(x+1)+" -j DROP")
            if x%2==1 and y%2==0:
                net.nameToNode["h"+str(x+1)].cmd("iptables -A OUTPUT -o h1-eth0 -d 10.0.0."+ str(y+1)+" -j DROP")
                net.nameToNode["h"+str(y+1)].cmd("iptables -A OUTPUT -o h1-eth0 -d 10.0.0."+ str(x+1)+" -j DROP")
    dumpNodeConnections(net.switches)
    CLI(net)

if __name__ == '__main__':
    snum = int(raw_input("number of switches : "))
    hnum = int(raw_input("number of hosts : "))
    topos = { 'mytopo': ( lambda: MyTopo( snum, hnum) ) }
    testTopo(snum, hnum)
