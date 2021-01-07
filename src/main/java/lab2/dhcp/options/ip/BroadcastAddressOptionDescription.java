package lab2.dhcp.options.ip;

import lab2.dhcp.ConfigurableOptionDescription;

public enum BroadcastAddressOptionDescription implements ConfigurableOptionDescription {
    INSTANCE;

    @Override
    public byte getType() {
        return 28;
    }

    @Override
    public String getName() {
        return "broadcast";
    }

    @Override
    public BroadcastAddressOption produce() {
        return new BroadcastAddressOption();
    }
}
