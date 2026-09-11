"""OpenFlow 1.3 learning switch used by the Phase 1 and 2 demos."""

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls


class GraphFlowSwitch13(simple_switch_13.SimpleSwitch13):
    """Learning switch that logs each connected datapath."""

    OFP_VERSIONS = [4]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        super().switch_features_handler(ev)
        self.logger.info("GraphFlow switch connected: datapath=%s", ev.msg.datapath.id)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, CONFIG_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        self.logger.info("GraphFlow datapath state changed: datapath=%s", datapath.id)
