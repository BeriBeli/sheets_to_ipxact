package org.example;

import javax.xml.namespace.QName;
import java.io.File;

import jakarta.xml.bind.*;

import org.example.IpXactVersion;

public class XmlGenerator {
    public static void generateXml(Object component, IpXactVersion version, String filePath) throws Exception {
        JAXBContext context = JAXBContext.newInstance(component.getClass());
        Marshaller marshaller = context.createMarshaller();
        marshaller.setProperty(Marshaller.JAXB_SCHEMA_LOCATION, version.getSchemaLocation());
        JAXBElement<?> componentElement = new JAXBElement<>(
                new QName(version.getNameSpace(), "component"),
                (Class<Object>) component.getClass(),
                component
        );
        marshaller.marshal(componentElement, new File(filePath));
        System.out.println("XML file generated successfully at: " + filePath);
    }
}