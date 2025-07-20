package org.example;

public enum IpXactVersion {
  IEEE_1685_2009(
    "1685-2009",
    "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009",
    "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009/index.xsd"
  ),
  IEEE_1685_2014(
    "1685-2014",
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2014",
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd"
  ),
  IEEE_1685_2022(
    "1685-2022",
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2022",
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2022/index.xsd"
  );

  private final String value;
  private final String nameSpace;
  private final String schemaLocation;

  IpXactVersion(String value, String nameSpace, String schemaLocation) {
      this.value = value;
      this.nameSpace = nameSpace;
      this.schemaLocation = schemaLocation;
  }

  public String getNameSpace() {
      return nameSpace;
  }

  public String getSchemaLocation() {
      return this.nameSpace + " " + this.schemaLocation;
  }

  public String value() {
      return value;
  }

  public static IpXactVersion fromValue(String version) {
      for (IpXactVersion v : IpXactVersion.values()) {
          if (v.value.equals(version)) {
              return v;
          }
      }
      throw new IllegalArgumentException("Unknown IP-XACT version: " + version);
    }
}