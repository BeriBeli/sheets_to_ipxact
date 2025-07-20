package org.example;

import org.example.schema.s1685_2014.*;
import jakarta.xml.bind.*;

import javax.xml.namespace.QName;
import java.io.File;

public class XmlGenerator {
    public static void generateXml(ComponentType component, String filePath) throws Exception {
        JAXBContext context = JAXBContext.newInstance(ComponentType.class);
        Marshaller marshaller = context.createMarshaller();
        marshaller.setProperty(Marshaller.JAXB_SCHEMA_LOCATION, "http://www.accellera.org/XMLSchema/IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd");
        JAXBElement<ComponentType> componentElement = new JAXBElement<>(
                new QName("http://www.accellera.org/XMLSchema/IPXACT/1685-2014", "component"),
                ComponentType.class,
                component
        );
        marshaller.marshal(componentElement, new File(filePath));
        System.out.println("XML file generated successfully at: " + filePath);
    }
}