import Form, { UiSchema } from "@rjsf/chakra-ui"
import { RJSFSchema } from "@rjsf/utils"
import { useEffect, useState } from "react"
import SimulationInputSchema from "./SimulationInput.json"
import validator from "@rjsf/validator-ajv8"
import { IChangeEvent } from "@rjsf/core"
import TitleFieldTemplate from "@components/form/templates/TitleFieldTemplate"
import { Accordion, Box, Heading, Spinner } from "@chakra-ui/react"
import { fetchUserAttributes } from "aws-amplify/auth/cognito"
import ObjectAccordionTemplate from "@components/form/templates/ObjectAccordionTemplate"

interface SimulationInputSchemaProps {
  queryCallback?: (data: FormValues) => void
}

export interface LatLong {
  lat: number
  lng: number
}

export interface FormLocation {
  lat: number
  long: number
}

enum GraphPerms {
  WRITE = "write",
  READ = "read",
}

export type GraphConfig = {
  name: string
  id: string
  perms?: Set<GraphPerms>
}

const center: LatLong = {
  lat: 54.97101,
  lng: -2.45682,
}

export interface FormValues {
  location: FormLocation
  fuel: { amount: number }
  query: { instance: string[] }
}

function SimulationInput({ queryCallback }: SimulationInputSchemaProps) {
  const [formSchema, setFormSchema] = useState<RJSFSchema>(structuredClone(SimulationInputSchema) as RJSFSchema)
  const [loc, setLoc] = useState<FormLocation>({ lat: center.lat, long: center.lng })
  const [lastManualUpdate, setLastManualUpdate] = useState<number>(Date.now())
  const [formData, setFormData] = useState<FormValues>({
    location: loc,
    fuel: { amount: 0 },
    query: { instance: ["default"] },
  })
  const [graphs, setGraphs] = useState<GraphConfig[]>([])
  const [loaded, setLoaded] = useState<boolean>(false)

  useEffect(() => {
    fetchUserAttributes().then((attributes) => {
      if ("custom:instances" in attributes && attributes["custom:instances"]) {
        const instances = JSON.parse(attributes["custom:instances"])
        if (Array.isArray(instances)) setGraphs(instances as GraphConfig[])
      } else {
        setLoaded(true)
      }
    })
  }, [])

  useEffect(() => {
    if (graphs.length > 0) {
      const schema = structuredClone(SimulationInputSchema as RJSFSchema)
      const query = (schema.definitions!["instanceInput"]! as RJSFSchema)!
      query["oneOf"] = [
        ...(query["oneOf"] as object[]),
        ...graphs.map((graph) => {
          return { const: graph.id, title: `${graph.name} 🔒` }
        }),
      ]
      setFormSchema(schema)
    }
    setLoaded(true)
  }, [graphs])

  const topLevelTitleSize = 22
  const uiSchema: UiSchema = {
    "ui:submitButtonOptions": {
      props: {
        className: "input-query-submit",
        style: { backgroundColor: "#39aed2", color: "white" },
      },
      submitText: "Evaluate using testbed",
    },
    location: {
      "ui:options": {
        columns: true,
        titleSize: topLevelTitleSize,
        map: true,
        mapTitle: "Project site",
      },
    },
    fuel: {
      "ui:options": {
        columns: false,
        titleSize: topLevelTitleSize,
      },
    },
    query: {
      "ui:options": {
        columns: false,
        titleSize: topLevelTitleSize,
      },
    },
  } as UiSchema

  const onSubmit = (data: IChangeEvent<any, RJSFSchema, any>) => {
    queryCallback && queryCallback(data.formData)
  }

  const setLocation = (newLocation: FormLocation | FormValues) => {
    const loc = "location" in newLocation ? (newLocation as FormValues).location : (newLocation as FormLocation)
    if ("lat" in loc && "long" in loc) setLoc(loc)
  }

  useEffect(() => {
    setFormData({ ...formData, location: loc })
  }, [loc])

  return !loaded ? (
    <Spinner />
  ) : (
    <Box>
      <Box mb={5}>
        <Heading as={"h2"} size={"lg"}>
          Project requirements
        </Heading>
      </Box>
      <Accordion allowMultiple defaultIndex={[0, 1]}>
        <Form
          formData={formData}
          schema={formSchema}
          uiSchema={uiSchema}
          validator={validator}
          onSubmit={onSubmit}
          formContext={{ setLocation, getLastManualUpdate: () => lastManualUpdate }}
          onChange={(e) => {
            setFormData(e.formData)
            setLastManualUpdate(Date.now())
          }}
          templates={{
            ObjectFieldTemplate: ObjectAccordionTemplate,
            TitleFieldTemplate: TitleFieldTemplate,
          }}
        />
      </Accordion>
    </Box>
  )
}

export default SimulationInput
