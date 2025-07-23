package org.example;

import javax.xml.namespace.QName;
import java.io.File;

import jakarta.xml.bind.*;

public class XmlGenerator {
    public static <T> void generateXml(T component, IpXactVersion version, String filePath) throws Exception {
        JAXBContext context = JAXBContext.newInstance(component.getClass());
        Marshaller marshaller = context.createMarshaller();
        marshaller.setProperty(Marshaller.JAXB_SCHEMA_LOCATION, version.getSchemaLocation());
        @SuppressWarnings("unchecked")
        JAXBElement<T> componentElement = new JAXBElement<>(
                new QName(version.getNameSpace(), "component"),
                (Class<T>) component.getClass(),
                component
        );
        marshaller.marshal(componentElement, new File(filePath));
    }
}