import Form, { UiSchema } from "@rjsf/chakra-ui"
import { RJSFSchema } from "@rjsf/utils"
import { useState } from "react"
import SimulationInputSchema from "./SimulationInput.json"
import validator from "@rjsf/validator-ajv8"
import { IChangeEvent } from "@rjsf/core"

interface SimulationInputSchemaProps {
  queryCallback?: (data: Record<string, any>) => void
}

function SimulationInput({ queryCallback }: SimulationInputSchemaProps) {
  const [formSchema, _] = useState<RJSFSchema>({ ...SimulationInputSchema } as RJSFSchema)

  const uiSchema = {
    "ui:submitButtonOptions": {
      submitText: "Query",
    },
  } as UiSchema

  const onSubmit = (data: IChangeEvent<any, RJSFSchema, any>) => {
    queryCallback && queryCallback(data.formData)
  }
  return <Form formData={{}} schema={formSchema} uiSchema={uiSchema} validator={validator} onSubmit={onSubmit} />
}

export default SimulationInput
