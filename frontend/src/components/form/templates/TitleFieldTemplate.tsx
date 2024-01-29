import { FormContextType, RJSFSchema, StrictRJSFSchema, TitleFieldProps, getUiOptions } from "@rjsf/utils"
import { Box, Divider, Heading } from "@chakra-ui/react"

export default function TitleFieldTemplate<
  T = any,
  S extends StrictRJSFSchema = RJSFSchema,
  F extends FormContextType = any
>({ id, title, uiSchema }: TitleFieldProps<T, S, F>) {
  const uiOptions = getUiOptions<T, S, F>(uiSchema)
  const titleSize = "titleSize" in uiOptions && uiOptions["titleSize"] ? `${uiOptions["titleSize"]}px` : undefined

  return (
    <Box id={id} mt={1} mb={4}>
      <Heading as="h5" fontSize={titleSize}>
        {title}
      </Heading>
      <Divider />
    </Box>
  )
}
