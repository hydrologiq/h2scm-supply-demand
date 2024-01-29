import Form, { UiSchema } from "@rjsf/chakra-ui"
import { RJSFSchema } from "@rjsf/utils"
import { useState } from "react"
import SimulationInputSchema from "./SimulationInput.json"
import validator from "@rjsf/validator-ajv8"
import { IChangeEvent } from "@rjsf/core"
import ObjectFieldTemplate from "@components/form/templates/ObjectFieldTemplate"
import TitleFieldTemplate from "@components/form/templates/TitleFieldTemplate"

interface SimulationInputSchemaProps {
  queryCallback?: (data: Record<string, any>) => void
}

function SimulationInput({ queryCallback }: SimulationInputSchemaProps) {
  const [formSchema, _] = useState<RJSFSchema>({ ...SimulationInputSchema } as RJSFSchema)

  const topLevelTitleSize = 22
  const uiSchema = {
    "ui:submitButtonOptions": {
      props: {
        className: "input-query-submit",
        style: { backgroundColor: "#39aed2", color: "white" },
      },
      submitText: "Query testbed",
    },
    location: {
      "ui:options": {
        columns: true,
        titleSize: topLevelTitleSize,
      },
    },
    fuel: {
      "ui:options": {
        columns: true,
        titleSize: topLevelTitleSize,
      },
    },
  } as UiSchema

  const onSubmit = (data: IChangeEvent<any, RJSFSchema, any>) => {
    queryCallback && queryCallback(data.formData)
  }
  return (
    <Form
      formData={{}}
      schema={formSchema}
      uiSchema={uiSchema}
      validator={validator}
      onSubmit={onSubmit}
      templates={{ ObjectFieldTemplate: ObjectFieldTemplate, TitleFieldTemplate: TitleFieldTemplate }}
    />
  )
}

export default SimulationInput
