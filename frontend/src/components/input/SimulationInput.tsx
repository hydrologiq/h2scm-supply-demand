import Form, { UiSchema } from "@rjsf/chakra-ui"
import { RJSFSchema } from "@rjsf/utils"
import { useState } from "react"
import SimulationInputSchema from "./SimulationInput.json"
import validator from "@rjsf/validator-ajv8"

function SimulationInput() {
  const [formSchema, setFormSchema] = useState<RJSFSchema>({ ...SimulationInputSchema } as RJSFSchema)

  const uiSchema = {
    "ui:submitButtonOptions": {
      submitText: "Query",
    },
  } as UiSchema

  return (
    <Form
      formData={{}}
      schema={formSchema}
      uiSchema={uiSchema}
      validator={validator}
      //   onSubmit={onSubmit}
    />
  )
}

export default SimulationInput
