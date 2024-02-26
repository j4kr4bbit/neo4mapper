from neo4j import GraphDatabase

# Connection setup and neo4j user/pw
neo4j_uri = "bolt://neo4j:7687"
neo4j_user = "neo4j"
neo4j_password = "test1234"  # Use your actual password

#driver which is needed in functions below as first arg
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))



def create_node(label: str, properties: dict=None, driver=driver):
    with driver.session() as session:
        # Convert properties dictionary to Cypher properties string
        properties_string = ', '.join([f"{key}: ${key}" for key in properties.keys()])
        cypher_query = (
            f"MERGE (n:{label} {{{properties_string}}}) RETURN n"
        )
        result = session.run(cypher_query, **properties)
        print(f"Node created with label {label} and properties {properties}.")
        return result.single()[0]



def create_or_merge_link_with_properties_and_direction(entity_id, link_name, rel_type, link_properties=None, direction="forward", driver=driver):
    """
    Creates or merges a link between two nodes with additional properties on the linked node
    and specifies the direction of the relationship.
    
    :param entity_id: ID of the entity node
    :param link_name: Name of the linked node
    :param rel_type: Type of the relationship
    :param link_properties: Properties to add to the linked node (default is None)
    :param direction: Direction of the relationship ("forward" or "reverse")
    :param driver: Neo4j driver instance
    """
    if link_properties is None:
        link_properties = {}
    with driver.session() as session:
        # Prepare the properties string for Cypher query
        properties_string = ', '.join(f'{key}: ${key}' for key in link_properties.keys())
        
        # Construct the Cypher query based on the direction
        if direction == "forward":
            query = (
                f"MATCH (e {{id: $entity_id}}) "
                f"MERGE (l:LinkedEntity {{name: $link_name, {properties_string}}}) "
                f"MERGE (e)-[:{rel_type}]->(l)"
            )
        elif direction == "reverse":
            query = (
                f"MATCH (e {{id: $entity_id}}) "
                f"MERGE (l:LinkedEntity {{name: $link_name, {properties_string}}}) "
                f"MERGE (l)-[:{rel_type}]->(e)"
            )
        else:
            raise ValueError("Invalid direction specified. Use 'forward' or 'reverse'.")
        
        # Execute the Cypher query
        session.run(query, entity_id=entity_id, link_name=link_name, **link_properties)
        print(f"Link of type '{rel_type}' {'from ' + str(entity_id) + ' to ' + link_name if direction == 'forward' else 'from ' + link_name + ' to ' + str(entity_id)} with properties {link_properties} created or merged successfully.")


def merge_relationship(node1_name, node2_name, direction, driver=driver):
    with driver.session() as session:
        if direction == "forward":
            query = (
                "MATCH (n1 {name: $node1_name}), (n2 {name: $node2_name}) "
                "MERGE (n1)-[:RELATES_TO]->(n2)"
            )
        elif direction == "reverse":
            query = (
                "MATCH (n1 {name: $node1_name}), (n2 {name: $node2_name}) "
                "MERGE (n2)-[:RELATES_TO]->(n1)"
            )
        else:
            raise ValueError("Invalid direction specified. Use 'forward' or 'reverse'.")
        
        session.run(query, node1_name=node1_name, node2_name=node2_name)
        print(f"Relationship {'from ' + node1_name + ' to ' + node2_name if direction == 'forward' else 'from ' + node2_name + ' to ' + node1_name} merged successfully.")



create_node('Entity', properties={
                'id': 1,
                'name': 'Entity',
                'affiliation': 'Affiliation', 
                'intention': 'Intention', 
                'threatLevel': 0, 
                'missionValue': 0, 
                'condition': 'Condition'
            })

create_node('Entity', properties={
                'id': 2,
                'name': 'Entity',
                'affiliation': 'Affiliation', 
                'intention': 'Intention', 
                'threatLevel': 0, 
                'missionValue': 0, 
                'condition': 'Condition'
            })

create_node('Entity', properties={
                'id': 3,
                'name': 'Entity',
                'affiliation': 'Affiliation', 
                'intention': 'Intention', 
                'threatLevel': 0, 
                'missionValue': 0, 
                'condition': 'Condition'
            })




create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="Track", rel_type="localizes", link_properties={"position": "NA", "orientation": "NA", "velocity": "NA", "velocity": "NA", "timestamp": "NA"}, direction="reverse")
create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="Facility1", rel_type="launchedFrom", link_properties={"location" : "NA", "Elevation": "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="Facility2", rel_type="recoversTo", link_properties={"location" : "NA", "Elevation": "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="ImageSensor", rel_type="recoversTo", link_properties={"pan" : "NA", "tilt": "NA", "zoom": "NA", "fov": "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="Action", rel_type="Issued", link_properties={"Type" : "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=1, link_name="OpArea", rel_type="entering", link_properties={"geoRect": "NA"}, direction="reverse")


create_or_merge_link_with_properties_and_direction(entity_id=2, link_name="Track", rel_type="localizes", link_properties={"position": "NA", "orientation": "NA", "velocity": "NA", "velocity": "NA", "timestamp": "NA"}, direction="reverse")
create_or_merge_link_with_properties_and_direction(entity_id=2, link_name="Jeep", rel_type="instanceOf", link_properties={"survivability" : "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=2, link_name="OpArea", rel_type="isWithin", link_properties={"geoRect": "NA"}, direction="reverse")


create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="Track", rel_type="localizes", link_properties={"position": "NA", "orientation": "NA", "velocity": "NA", "velocity": "NA", "timestamp": "NA"}, direction="reverse")
create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="Target", rel_type="hasQualifier", link_properties={"priority" : "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="RcCar", rel_type="instanceOf", link_properties={"lethality" : "NA", "threatRange": "NA"})
create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="OpArea", rel_type="isWithin", link_properties={"geoRect": "NA"}, direction="reverse")
create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="Contactreport", rel_type="observationOf", link_properties={"contactType": "NA", "confidence": "NA", "position": "NA", "timestamp": "NA"}, direction="reverse")
create_or_merge_link_with_properties_and_direction(entity_id=3, link_name="Action", rel_type="hasObject", link_properties={"Type" : "NA"}, direction="reverse")


